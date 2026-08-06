# Olist-Sales-Analysis
Analysis of publicly available sales data from Olist

```mermaid
erDiagram
	CUSTOMER ||--o{ ORDER : connection_label
	CUSTOMER {
		datatype name_of_column
		string name
		int custNumber
	}
```

