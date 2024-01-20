import telebot
from PIL import Image
import numpy as np
from tensorflow import keras
import io  # импортировать модуль io для работы с потоками байтов

bot = telebot.TeleBot('your_token')
model = keras.models.load_model('my_model.keras')

# Start
@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}! Вам нужно отправить изображение с арбузом, сорт которого вы хотите определить, нейросеть даст вам ответ, к которому наиболее склонна.')

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # Получаем информацию о изображении
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)

    # Преобразуем изображение в массив numpy
    image = Image.open(io.BytesIO(file))
    image = image.resize((128, 128))  # Здесь нужно убедиться, что изображение соответствует размеру, на котором обучалась модель
    image = np.array(image) / 255.0

    # Предсказываем класс изображения с помощью загруженной модели
    prediction = model.predict(np.array([image]))
    predicted_class = np.argmax(prediction)

    # Отправляем ответ пользователю с предсказанным классом
    bot.send_message(message.chat.id, f"This looks like class {predicted_class}")

    class_messages = {
        0: "",
        1: "",
        2: "",
        3: "",
        4: "",
        5: "",
        6: "",
        7: "",
        8: "",
        9 : "",
        10: "",
        11: "",
        12: "",
        13: "",
        14: "",
        15: "",
        16: "",
        17: "",
        18: "",
        19: "",
        20: "",
        21: "",
        22: ""
        # Добавьте другие классы и соответствующие им сообщения здесь
    }

    if predicted_class in class_messages:
        message1 = class_messages[predicted_class]
        bot.send_message(message.chat.id, message1)  # Отправляем сообщение о предсказанном классе непосредственно пользователю
    else:
        bot.send_message(message.chat.id, "Нет информации для этого класса.")

bot.polling(none_stop=True)