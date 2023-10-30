import os.path

from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с ожидаемым результатом
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что на запрос всех питомцев возвращается не пустой список.
    Для этого сначала получаес api ключ и сохраняем его в переменную auth_key. Далее, используя этот ключ, запрашиваем
    список всех питомцев и проверяем, что он не пустой. Доступные занчения для параметра filter: 'my_pets или '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='George', animal_type='cat', age='10', pet_photo='images/George.jpeg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Барсик', animal_type='коть', age='8'):
    """Проверяем, что можно обновить данные питомца из списка своих питомцев"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то вызываем исключение с текстом об отсутствии своих питомцев
        raise Exception('There is no My pets')


def test_successful_delete_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, если список своих питомцев пустой, то добавляем нового и опрять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_info_about_new_pet(auth_key, 'Барсик', 'кот', '8', 'images/Barsik.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.detele_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, что статус ответа 200 и в списке питомцев не id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_create_a_pet(name='Жоржик', animal_type='кот', age='13'):
    """Проверяем возможность добавления нового питомца(без фото)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_add_photo(pet_photo='images/George.jpeg'):
    """Проверяем возможность добавить фото питомца"""

    # Запрашиваем ключ api и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, пробуем добавить фото для первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception('There is no My pets')


def test_get_auth_key_with_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что при вводе неверного пароля система выдаст ошибку"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_negative_add_pet_age_not_int(name='Пушок', animal_type='кот', age='два'):
    """Проверяем, что при вводе возраста не числом система выдаст ошибку"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert type(result['age']) != int


def test_add_photo_wrong_extension(pet_photo='images/cat.png'):
    """Проверяем, что при загрузке фото с неверным расширением файла система выдаст ошибку"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 500
    else:
        raise Exception('There is no My pets')


def test_update_only_name(name='Барсик', animal_type='', age=''):
    """Проверяем, что можно изменить только имя питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no My pets')


def test_get_auth_key_for_unregistered_user(email=invalid_email, password=invalid_password):
    """Проверяем, что при вводе незарегистрированного email и пароля система выдаст ошибку"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_add_new_pet_without_name(animal_type='cat', age='10', pet_photo='images/George.jpeg'):
    """Проверяем, что при попытке создания питомца без обязательного поля Имя система выдаст ошибку"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_info_about_new_pet(auth_key, name=None, animal_type=animal_type, age=age, pet_photo=pet_photo)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    assert status == 400


def test_get_auth_key_with_blank_fields():
    """Проверяем, что при попытке получить ключ с пустыми полями email и пароль система выдаст ошибку"""

    status, result = pf.get_api_key(email=None, password=None)
    assert status == 403


def test_add_pet_simple_with_blank_fields():
    """Проверяем, что при попытке создать питомца, не заполняя все обязательные поля(name, animal_type и age)
    система выдаст ошибку"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name=None, animal_type=None, age=None)
    assert status == 400

