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
* Появился нормальный `Readme.md` (надеюсь)
* Ну и pep8 и прочие

## В планах

* Добавить какой нибудь еще метод стеганографии
    * Хитрый LSB где будет примерно такой формат данных
      `[header | length of key | key(maybe encoded) | data+message]`
    * Эхо-метод
* Кодирование и\или криптографирование сообщения
* _Возможно_ анализ сообщения на этапе скрытия
* Сделать что нибудь с исходниками gtk-клиента,
  впервые писал gui не в вебе, код получился прямо скажем не очень
* _`cli`_: Уведомление о необходимости `--message \ -m` аргумента, если выбран режим работы: `hide`

## Порядок работы
### CLI-клиент

* Запустить `python3 -m stegapy.client.cli -h`
  и ознакомится с нужными аргументами и их порядком, на всякий случай листинг ниже
```
    usage: stegapy.client.cli [-h] {WAV} input {LSB} {hide,unhide} ... output

    positional arguments:
      {WAV}          container format
      input          path to container file
      {LSB}          steganography method
      {hide,unhide}  sub-command help
        hide         Hiding work mode
        unhide       Unhide work mode
      output         Output file

    optional arguments:
      -h, --help     show this help message and exit


    Copyright 2014 Maxim Syrykh
```
* Запустить `python3 -m stegapy.client.cli` с нужными аргументами
  Например:
```
python3 -m stegapy.client.cli WAV test.wav LSB hide sign.png o.wav
```
* ...
* PROFIT

### GUI-клиент (GTK+3)
* Запустить `python3 -m stegapy.client.gtk`
* Используя максимально интуитивно понятный интерфейс сделать свои дела
* ...
* PROFIT
