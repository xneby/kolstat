Graf do plannera - opis formatu TTF
===================================

Wstęp
========

Graf do plannera nie jest zbyt skomplikowany. Wierzchołkami tego grafu są przystanki i stacje kolejowe, a z wierzchołka A do B istnieje krawędź wtedy i tylko wtedy, gdy istnieje pociąg, dla którego A i B są **kolejnymi** stacjami zatrzymania. Każda krawędź pamięta wszystkie pociągi (a raczej przejazdy pociągów), które powodują istnienie tej krawędzi.

Opis formatu
===============

Nagłówek
-------------

Na nagłówek składają się cztery pola:

    struct ttf_header {
        [unsigned] int           magic,
                   int           creation_time,
                   int           num_vertices,
                   int           num_edges
    }

magic (w obecnej wersji formatu) to 809915476 ("TTF0").
creation_time to czas utworzenia w formacie Unix timestamp.
num_vertices to liczba wierzchołków grafu.
num_edges to liczba krawędzi grafu.

**Uwaga**. Wierzchołki grafu muszą mieć numer taki jak pole Station.id w bazie danych. Więc może się zdażyć, że trzeba będzie sztucznie zwiększyć pole num_vertices.

Graf
---------

Po nagłówku występuje opis grafu. Opis grafu to V-krotnie powtórzony opis wierzchołka. Na opis wierzchołka składa się nagłówek opisu oraz lista krawędzi.

    struct ttf_vertex_header {
        [unsigned] int           degree
    }

degree to stopień (liczba krawędzi wychodzących) wierzchołka

Po nałówku opisu wierzchołka występuje lista krawędzi. Każda to

    struct ttf_vertex_edge {
        [unsigned] int           destination,
        [unsigned] int           identifier
    }

destination to numer wierzchołka, do którego krawędź prowadzi.
identifier to identyfikator krawędzi (Przyda się w następnej sekcji).

identifier jest numerowany od jedynki.

Opis kawędzi
------------

Po opisie grafu następuje opis krawędzi. Krawędzie są opisywane zgodnie z kolejnością identyfikatorów. Każdy opis składa się z nagłówka opisu i listy pociągów.

    struct ttf_edge_header {
        [unsigned] int           num_trains
    }

num_trains to liczba pociągów ,,realizująych'' krawędź.

Po nagłówku opisu krawędzi występuje lista pociągów. Każdy pociąg to sześć pól:

    struct ttf_edge_train {
        [unsigned] int           dep_station,
        [unsigned] int           arr_station,
        [unsigned] int           dep_time,
        [unsigned] int           arr_time,
        [unsigned] int           dep_stop,
        [unsigned] int           arr_stop
    }

Pola z prefiksem dep_ dotyczą odjazdu, a pola z prefiksem arr_ dotyczą przyjazdu. Pola z sufiksem _station oznaczają nr stacji, pola z sufiksem _time oznaczają czas - liczbę minut od początku rozkładu jazdy, a pola z sufiksem _stop oznaczają id odpowiedniego rekordu TrainStop z bazy danych.

Przykłady
=========

Przykładowy skrpyt w pythonie generujący plik według powyższego opisu znajduje się w kolstatapp/planner/graph_gen/, a kod plannera odpowiadający za czytanie tego pliku znajduje się w kolstatapp/planner/dijkstra.cpp .
