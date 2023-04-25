from typing import Generator

class TableGatewayInterface():
    """
    Interface for TableGateway that implements execution of select execution.
    """
    def select(self)->Generator:
        raise NotImplementedError()
    def execute_select(self)->Generator:
        """
        public Method that implement user input with select
        :return: generate response serialized for tables 
        """
        params=[]
        for param in self.select.__code__.co_varnames[1:-1]:
            result = input(f'{param}:').strip()
            params.append(result if result!=''else '%')
        yield [True] +self.to_string
        for results in self.select(*params):
            yield [False] +list(results)

class RowGatewayInterface():
    """
    Interface for RowGateway that implements execution of insert/update/delete.
    """
    def insert(self)->list:
        raise NotImplementedError()
    def update(self)->list:
        raise NotImplementedError()
    def delete(self)->list:
        raise NotImplementedError()
    def execute_insert(self)->list:
        """
        public Method that implement user input with insert method
        :return: result of inserting
        """
        params=[]
        for param in self.insert.__code__.co_varnames[1:]:
            result = input(f'{param}:').strip()
            params.append(result if result!=''else '%')
        return self.insert(*params)
    def execute_update(self)->list:
        """
        public Method that implement user input with insert method
        :return: result of updating
        """
        params=[]
        for param in self.update.__code__.co_varnames[1:]:
            result = input(f'{param}:').strip()
            params.append(result if result!=''else '%')
        return self.update(*params)
    def execute_delete(self)->list:
        """
        public Method that implement user input with insert method
        :return: result of deleting
        """
        params=[]
        for param in self.delete.__code__.co_varnames[1:]:
            result = input(f'{param}:').strip()
            params.append(result if result!=''else '%')
        return self.delete(*params)