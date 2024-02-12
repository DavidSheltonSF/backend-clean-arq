from typing import Type, Dict, List
from src.data.find_user import FindUser
from src.domain.use_cases import RegisterPet as RegisterPetInterface
from src.data.interfaces import PetRepositoryInterface as PetRepository
from src.domain.models import Pets, Users


class RegisterPet(RegisterPetInterface):
    """RegisterPet use case

    Args:
        RegisterPetInterface (_type_): _description_
    """

    def __init__(self, pet_repository: Type[PetRepository], find_user: Type[FindUser]):
        self.pet_repository = pet_repository
        self.find_user = find_user

    def register(
        self,
        pet_name: str,
        specie: str,
        user_information: Dict[int, str],
        age: int = None,
    ) -> Dict[bool, Pets]:
        """Register pet

        Args:
            pet_name (str): Pet's name
            specie (str): Pet's specie
            age (int): Pet's age
            user_information (Dict[int, str]): Dictionary with
            user_id and/or name

        Returns:
            Dict[bool, pets]: Dictionary with imformation of the process
        """

        response = None

        validate_entry = (
            isinstance(pet_name, str)
            and isinstance(specie, str)
            and (isinstance(age, int) or age is None)
            and isinstance(user_information, dict)
        )
        # Try to find the user
        user = self.__find_user_information(user_information)

        # Check validate_entry and user found
        checker = validate_entry and user["Success"]

        if checker:
            response = self.pet_repository.insert_pet(
                pet_name, specie, age, user_information
            )

        return {"Success": checker, "Data": response}

    def __find_user_information(
        self, user_information: Dict[int, str]
    ) -> Dict[bool, List[Users]]:
        """Check user infos and select user

        Args:
            user_information (Dict[int, str]): Dictionary with
            user_id and/or name

        Returns:
            Dict[bool, List[Users]]: Dictionary with the response
            of find_user use case
        """

        user_founded = None
        user_params = user_information.keys()

        # Check if user_id  and user_name is in params
        if "user_id" in user_params and "user_name" in user_params:
            user_founded = self.find_user.by_id_and_name(
                user_id=user_information["user_id"],
                user_name=user_information["user_name"],
            )

        # Check if user_id is in params and user_name is not
        elif "user_id" in user_params and "user_name" not in user_params:
            user_founded = self.find_user.by_id(user_information["user_id"])

        # Check if user_id is not in params and user_name is in
        elif "user_id" not in user_params and "user_name" in user_params:
            user_founded = self.find_user.by_name(user_information["user_name"])

        # In last case
        else:
            return {"Success": False, "Data": None}

        return user_founded
