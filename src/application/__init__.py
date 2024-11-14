import typing

InputDTO = typing.TypeVar("InputDTO", contravariant=True)
OutputDTO = typing.TypeVar("OutputDTO", covariant=True)


class UseCase(typing.Protocol[InputDTO, OutputDTO]):
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError
