## UML‍ 💬:

Heres the UML that represents how the application works with their classes.

```mermaid
classDiagram

  class search_algorithm {
    - nome: String
    + fazerBarulho(): void
  }

  class wind_aco {
    - amamenta: boolean
    + produzLeite(): void
  }

  class wind_trangenic1{
    - voa: boolean
    + voar(): void
  }

  class wind_trangenic2{
    + late(): void
  }

  class wind_trangenic3{
    + mia(): void
  }

  search_algorithm <|-- wind_trangenic3
  search_algorithm <|-- wind_trangenic2
  search_algorithm <|-- wind_trangenic1
  search_algorithm <|-- wind_trangenic
  search_algorithm <|-- wind_aco
```

## Classes 🎒: