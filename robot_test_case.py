import contextlib
import gc
import threading
import typing
import unittest
import weakref
from typing import Type, Literal

import hal
import hal.simulation
import ntcore
import pytest
import wpilib
import wpilib.simulation
import wpilib.shuffleboard
from wpilib.simulation import DriverStationSim, stepTiming, stepTimingAsync, pauseTiming, restartTiming

try:
    import commands2
except ImportError:
    commands2 = None


# https://github.com/robotpy/pyfrc/blob/main/pyfrc/test_support/pytest_plugin.py

class RobotTestCase(unittest.TestCase):
    robot_class: Type[wpilib.RobotBase]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class TestRobot(self.robot_class):
            def robotInit(self):
                try:
                    super().robotInit()
                finally:
                    self.__robotInitialized()

        TestRobot.__name__ = self.robot_class.__name__
        TestRobot.__module__ = self.robot_class.__module__
        TestRobot.__qualname__ = self.robot_class.__qualname__

        self.__wrapped_robot_class = TestRobot

    def setUp(self):
        self.__nt_inst = ntcore.NetworkTableInstance.getDefault()
        self.__nt_inst.startLocal()

        pauseTiming()
        restartTiming()

        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        DriverStationSim.setAutonomous(False)
        DriverStationSim.setEnabled(False)
        DriverStationSim.notifyNewData()

        self.__robot = self.__wrapped_robot_class()
        self.robot = weakref.proxy(self.__robot)
        self.controller = TestController(self.robot)

    def tearDown(self):
        wpilib.simulation._simulation._resetMotorSafety()

        del self.__robot
        del self.robot
        del self.controller

        if commands2 is not None:
            commands2.CommandScheduler.resetInstance()

        gc.collect()

        # shutdown networktables before other kinds of global cleanup
        # -> some reset functions will re-register listeners, so it's important
        #    to do this before so that the listeners are active on the current
        #    NetworkTables instance
        self.__nt_inst.stopLocal()
        self.__nt_inst._reset()

        # Cleanup WPILib globals
        # -> preferences, SmartDashboard, Shuffleboard, LiveWindow, MotorSafety
        wpilib.simulation._simulation._resetWpilibSimulationData()
        wpilib._wpilib._clearSmartDashboardData()
        wpilib.shuffleboard._shuffleboard._clearShuffleboardData()

        # Cancel all periodic callbacks
        hal.simulation.cancelAllSimPeriodicCallbacks()

        # Reset the HAL handles
        hal.simulation.resetGlobalHandles()

        # Reset the HAL data
        hal.simulation.resetAllSimData()


class TestController:
    """
    Use this object to control the robot's state during tests
    """

    def __init__(self, robot: wpilib.RobotBase):
        self._thread: typing.Optional[threading.Thread] = None
        self._robot = robot

        self._cond = threading.Condition()
        self._robot_started = False
        self._robot_initialized = False
        self._robot_finished = False

    def _on_robot_initialized(self):
        with self._cond:
            self._robot_initialized = True
            self._cond.notify_all()

    def _robot_thread(self, robot):
        with self._cond:
            self._robot_started = True
            self._cond.notify_all()

        assert robot is not None  # shouldn't happen...

        robot._TestRobot__robotInitialized = self._on_robot_initialized

        try:
            robot.startCompetition()
            assert self._robot_finished
        finally:
            # always call endCompetition or python hangs
            robot.endCompetition()
            del robot

    @contextlib.contextmanager
    def run_robot(self):
        """
        Use this in a "with" statement to start your robot code at the
        beginning of the with block, and end your robot code at the end
        of the with block.

        Your `robotInit` function will not be called until this function
        is called.
        """

        # remove robot reference so it gets cleaned up when gc.collect() is called
        robot = self._robot
        self._robot = None

        self._thread = th = threading.Thread(
            target=self._robot_thread, args=(robot,), daemon=True
        )
        th.start()

        with self._cond:
            # make sure the thread didn't die
            assert self._cond.wait_for(lambda: self._robot_started, timeout=1)

            # If your robotInit is taking more than 2 seconds in simulation, you're
            # probably doing something wrong... but if not, please report a bug!
            assert self._cond.wait_for(lambda: self._robot_initialized, timeout=2)

        try:
            # in this block you should tell the sim to do sim things
            yield
        finally:
            self._robot_finished = True
            robot.endCompetition()

        # Increment time by 1 second to ensure that any notifiers fire
        stepTimingAsync(1.0)

        # the robot thread should exit quickly
        th.join(timeout=1)
        if th.is_alive():
            pytest.fail("robot did not exit within 2 seconds")

        self._robot = None
        self._thread = None

    @property
    def robot_is_alive(self) -> bool:
        """
        True if the robot code is alive
        """
        th = self._thread
        if not th:
            return False

        return th.is_alive()

    def run_mode(
            self,
            mode: Literal["auto", "teleop", "disabled"],
            seconds: float,
            assert_alive: bool = True,
    ) -> float:
        assert self.robot_is_alive, "did you call control.run_robot()?"

        assert seconds > 0

        DriverStationSim.setDsAttached(True)
        DriverStationSim.setAutonomous(mode == "auto")
        DriverStationSim.setEnabled(mode != "disabled")

        tm = 0.0

        while tm < seconds + 0.01:
            DriverStationSim.notifyNewData()
            stepTiming(0.05)
            if assert_alive:
                assert self.robot_is_alive
            tm += 0.05

        return tm
