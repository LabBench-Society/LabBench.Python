from labbench_comm.devices.lio.functions.base import _LIOFunction


class Stop(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x20

    def __init__(self) -> None:
        super().__init__(request_length=1, response_length=0)
        self.reset_programs = False

    @property
    def reset_programs(self) -> bool:
        return self.request.get_bool(0)

    @reset_programs.setter
    def reset_programs(self, value: bool) -> None:
        self.request.insert_bool(0, value)

    def __str__(self) -> str:
        return "[0x20] Stop"
