# Стеганография в WAV

## Что-нового

* Принципиально новая архитектура приложения
    * Декомпозиция кода
    * Обработка ошибок
    * Хитрый импорт только необходимых внутренних библиотек
* Теперь задача решается без использования модуля `wave`
    * В обычных `PCM` контейнерах гарантируется невидимость данных
    * В остальных форматах возможны повреждения мета-данных и\или сильное повреждение контента
* Переписал тесты
* Новый cli-клиент:
    * Парсинг аргументов с помощью `argparse`
    * Теперь есть help
* Новый gui-клиент:
    * GTK+3
    * Больше возможностей чем в cli-клиенте
* Красивая документация, спасибо, `pycco`


## Порядок работы
* Запустить `python3 -m stegapy -h`
