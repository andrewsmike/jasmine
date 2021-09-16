# Jasmine SQL: parse, reformat, manipulate, and analyze SQL queries.


# TODO
- Real pretty printing and serialization defaults for SemanticTrees
- Debug current SemanticNode issues
- Add semantic nodes for core query
- Add SemanticTree / ParserTree / expr scanning? (Hmmm....)
- Pretty printing: handle joins properly
- Pretty printing: handle UNIONs properly


## Known query manipulation use-cases
- Push down workunit constraint (SQL engine has this?) (Add appropriate WHERE)
- Derive scheduling query  (Pretty substantial restructure. Useful in snowflake?)
- - Scheduling query as DB trigger?
- Merge into <=> update <=> insert <=> etc  #  Add appropriate WHERE clause
- Switch out tables for staging tables, tables with multiple versions (Maybe add JOIN clauses, replace data)
- Add JOINs to tables (Add JOIN clause, substitute SELECT exprs)
- Add _denormalizations_?  (Add JOIN clause, substitute SELECT exprs)
