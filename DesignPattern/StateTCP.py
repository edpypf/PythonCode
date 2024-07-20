from enum import Enum, auto

class TCPStateEnum(Enum):
    CLOSED = auto()
    LISTENING = auto()
    ESTABLISHED = auto()

from abc import ABC, abstractmethod

class TCPState(ABC):
    @abstractmethod
    def open(self, context: 'TCPConnection') -> None:
        pass

    @abstractmethod
    def close(self, context: 'TCPConnection') -> None:
        pass

    @abstractmethod
    def send(self, context: 'TCPConnection', data: str) -> None:
        pass

class ClosedState(TCPState):
    def open(self, context: 'TCPConnection') -> None:
        print('Opening connection...')
        context.set_state(TCPStateEnum.LISTENING)

    def close(self, context: 'TCPConnection') -> None:
        print('Connection is already closed.')

    def send(self, context: 'TCPConnection', data: str) -> None:
        print('Cannot send data, connection is closed.')

class ListeningState(TCPState):
    def open(self, context: 'TCPConnection') -> None:
        print('Connection is already open and listening.')

    def close(self, context: 'TCPConnection') -> None:
        print('Closing connection...')
        context.set_state(TCPStateEnum.CLOSED)

    def send(self, context: 'TCPConnection', data: str) -> None:
        print('Cannot send data, connection is not established.')

class EstablishedState(TCPState):
    def open(self, context: 'TCPConnection') -> None:
        print('Connection is already established.')

    def close(self, context: 'TCPConnection') -> None:
        print('Closing connection...')
        context.set_state(TCPStateEnum.CLOSED)

    def send(self, context: 'TCPConnection', data: str) -> None:
        print(f'Sending data: {data}')

class TCPConnection:
    def __init__(self):
        self.states = {
            TCPStateEnum.CLOSED: ClosedState(),
            TCPStateEnum.LISTENING: ListeningState(),
            TCPStateEnum.ESTABLISHED: EstablishedState(),
        }
        self.current_state = self.states[TCPStateEnum.CLOSED]

    def set_state(self, state: TCPStateEnum) -> None:
        self.current_state = self.states[state]

    def open(self) -> None:
        self.current_state.open(self)

    def close(self) -> None:
        self.current_state.close(self)

    def send(self, data: str) -> None:
        self.current_state.send(self, data)

if __name__ == '__main__':
    connection = TCPConnection()
    
    connection.open()      # Transition to ListeningState
    connection.send('Hello')  # Cannot send data in ListeningState
    connection.close()    # Transition to ClosedState
    connection.open()      # Transition to ListeningState
    connection.open()      # Already in ListeningState
    connection.send('Hello')  # Cannot send data in ListeningState
    connection.close()    # Transition to ClosedState
    connection.open()      # Transition to ListeningState
    connection.open()      # Transition to EstablishedState
    connection.send('Hello')  # Send data in EstablishedState
