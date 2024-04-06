from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_cannot_get_api_key_no_password (email=valid_email, password=''):
    """ 1. Проверяем что запрос api ключа без пароля возвращает статус 403
    и в результате не содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result



def test_cannot_get_api_key_wrong_password (email=valid_email, password='******'):
    """ 2. Проверяем что запрос api ключа с некорректным паролем возвращает статус 403
    и в результате не содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result



def test_create_pet_simple (name='Мася', animal_type='котейка', age='3'):
    """3. Проверяем что можно добавить питомца с корректными данными без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name



def test_cannot_create_pet_simple_no_data (name='', animal_type='', age=''):
    """4. Проверяем что нельзя добавить питомца без имени, типа и возраста (по факту - можно)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status != 200



def test_add_photo (pet_photo='images/cat1.jpg'):
    """5. Проверяем, что можно добавить фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем cписок питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем ну пусть ли список и добавляем фото питомца на сервер первому пету в списке
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet (auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 200
    assert 'pet_photo' in result



def test_cannot_add_photo_gif (pet_photo='images/cat2.gif'):
    """6. Проверяем, что нельзя добавить фото питомца в формате gif"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем cписок питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем ну пусть ли список и добавляем фото питомца на сервер первому пету в списке
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet (auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 500



def test_cannot_delete_self_pet_no_authorisation ():
    """7. Проверяем, что нельзя удалить питомца с пустым ключом авторизации"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Камикадзе", "кот", "10", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # подставляем пустой ключ авторизации
    auth_key = {'key': ''}

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 403


def test_cannot_add_new_pet_with_negative_age (name='Негатив', animal_type='Мистер', age='-10', pet_photo='images/cat1.jpg'):
    """8. Проверяем, что нельзя добавить питомца с отрицательным возрастом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200



def test_cannot_add_new_pet_no_data (name='', animal_type='', age='', pet_photo='images/cat1.jpg'):
    """9. Проверяем, что нельзя добавить питомца без имени, типа и возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200



def test_cannot_update_self_pet_info_no_data (name='', animal_type='', age=''):
    """10. Проверяем, что нельзя передать во все поля питомца пустые значения"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status != 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
