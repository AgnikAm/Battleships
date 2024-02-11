0. Ogólne:
    * Brak typowania (typy to łatwiejsze życie, bardziej eleganckie i zrozumiałe API...); nie wiem co jest czym i muszę robić reverse engineering całego projektu ;v
    * Informacja o stanie gry jest niejawna; fajnie byłoby zrobić enum z nazwami stanów i używać go w logice aplikacji
    * Statki warto trzymać w hashmapie (lista też jest potrzebna, ale nie wystarczy)
    * event.type == coś w każdej gałęzi ifa...  (patrz punkt o match statement poniżej)
    * Projekt nieustrukturyzowany - kod źródłowy miesza się z assetami...

1. game:
    * Czemu wszystko pływa w powierzu a nie przynależy do klasy...
    * Ładniej obsługiwać eventy match statementem a nie litanią ifów
    * Mając klasę łatwiej wyłączyć z kodu powtarzalne kawałki i w ogóle podzielić go na metody
    * łatwiej przechować stan gry...
    * Pętla z while(True) i sys(exit) to fatalne rozwiązanie. Lepiej utrzymywać stan aplikacji w zmiennej w stylu "running: bool = True" i modyfikować jej wartość w handlerach odpowiednich zdarzeń
    * Można też zrobić to pozycją w enumie wspomnianym wyżej

2. game_board:
    * Czym są x i y w konstruktorze?
    * nazwa metody draw_board w klasie Game**BOARD** jest nadmiarowa - wystarczyłoby samo "draw"
    * align_axes można bardziej rozdrobnić - osobne metody align_rows i align_cols, może uda się to ujednolicić czy wyodrębnić wspólne elementy
    * place_ships bym przerobił w całości - dodał metodę "place_ship" i wołał ją z głównej pętli pygame z obsługą eventów
    * Podział eventów na dwa kawałki kodu to zła decyzja w designie - klasy powinny być *single responsibility*. Wszystkie eventy obsłuż w głównej pętli
    * Pisanie tekstu na ekran też powinno być w game.py
    * Pętla po rozmiarach też..
    * Jeśli już chcesz mieć moduł "draw_functions" to umieść w nim **wszystko** co służy do rysowania