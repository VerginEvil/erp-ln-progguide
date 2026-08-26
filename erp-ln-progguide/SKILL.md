---
name: erp-ln-progguide
description: Infor ERP LN / Baan 4GL programmer's reference. Use when writing, reading, or debugging Baan/LN 4GL (bshell) code, 4GL session scripts, DAL scripts, AFS/function-server automation, report scripts, LN SQL queries, bshell built-in functions, predefined variables, debugger usage, resolving SQL error states (SQLSTATE), or developing Infor LN extensions (Extension Modeler, CDFs, table/session/report/BOD/OData/menu/process extension points and their hooks) in ttadv / Infor Studio / LN Cloud.
---

# Infor ERP LN Programmer's Guide (Baan 4GL)

Full text of the official Infor *Programmer's Guide* (`progguide 10.8.12pre en`) plus its *SQL* volume and the *Infor LN Extensions Development Guide 10.8*, converted to plain Markdown: **2,906 + 155 + 162 pages**, including **2,366 bshell function references** with syntax, arguments, return values, context, and examples.

## How to answer questions (token-efficient workflow)

Never read folders blindly. Use this order:

1. **Known function name** -> grep `references/FUNCTION_INDEX.md` for the name.
   Each line has the normalized signature and the exact `.md` path. Then Read only that file.
2. **Free-text question** ("how to open a file", "utc conversion", "query hint", "before.save.object hook") -> run:
   ```
   python <skill_dir>/scripts/search.py <terms> [--dir guide|sql|extensions|all] [--group substr] [--regex PATTERN] [--max 25]
   python <skill_dir>/scripts/search.py --list-groups        # topic folders + page counts
   ```
   Output is `file:line: snippet` matches ranked by hits. Read only promising files.
3. **All pages** -> `index/INDEX.tsv` maps every page path to its title.
4. Links between pages are relative Markdown links and resolve correctly; follow them by Reading the target path next to the current file.

## Layout

```
references/
  guide/progguide/            main guide, mirrored from original TOC
    3gl_features/             data types, variables, expressions, multibyte/UTC
    4gl_features/             4GL sections: program/form/group/field/choice/event/
                              zoom, main.table.io subsections, flow of standard program
    bol/                      Business Object Layer programming
    functions_<topic>/        ~130 function groups; each has overview.md,
                              synopsis.md (all signatures), one page per function
    multitasking/ events/     process model, event handling
    debugger/ profiler/       baan debugger commands, call graph profiler
    misc/                     bshell options/env vars/resources, predefined vars,
                              known limits, ASCII/Unicode encodings
    errors/                   Infor ES error messages
    glossary/
  sql/progguide/
    functions_database_handling/   LN SQL (Baan SQL): SELECT/FROM/WHERE/GROUP BY/
                                   predicates, expressions, data types, reserved words
    sql_states_and_messages/       SQLSTATE codes explained (e.g. 22001, 42I01)
  extensions/                 Infor LN Extensions Development Guide (10.8), one file
                              per chapter; start at references/EXTENSIONS_INDEX.md
index/INDEX.tsv               every page: path TAB title
references/FUNCTION_INDEX.md  all 2366 functions grouped by topic, grep this first
references/EXTENSIONS_INDEX.md chapter list + orientation for the extensions guide
scripts/search.py             full-text search tool (stdlib Python only)
```

## Baan 4GL crash course

- **Runtime**: programs execute in the *bshell*. UI runs in WebUI / LN UI. Development happens in Infor Studio (ttadv) under VRC version control.
- **Script types**: `type 1-4` 4GL UI session scripts (init.form, before.display, main.table.io...), 3GL scripts, DAL scripts (data access layer hooks per table), libraries (`bic_*` DLLs), report scripts, and Function Server / AFS automation (`function.server.*`, `stpapi.*` style calls).
- **Data types**: `long`, `double`, `string len [fixed]`, `domain`, `table`, `xml node`, UTC date/time via `utc.*`; doubles need care (`double.cmp()`).
- **Database access**: embedded Baan SQL with `SELECT ... FROM ... WHERE ... SELECTDO ... SELECTEOS ... ENDSELECT`, `db.insert/db.update/db.delete`, transaction control `commit.transaction()`, `abort.transaction()`, `retry.point()`.
- **Tables**: named `<package><module><seq>` e.g. `tiitm001` (item master), fields referenced directly; referential info in runtime dictionary (`rdi.*` functions).
- **Query extensions**: `query.extend.where()/.select()/.from()` modify generated session queries.
- **Predefined variables**: see `guide/progguide/misc/predefined_variables.md`.
- **LN Extensions** (Extension Modeler): customize standard components without code changes to them. Extension points: domain, table, report, session, BOD/BDE, OData REST, menu, process. Hooks are `function extern` DAL-style functions (e.g. `before.save.object(long mode)`, `method.is.allowed()`, `<field>.check.input()`, `before.context.send()`); errors via `dal.set.error.message("@...")` + `DALHOOKERROR`. CDFs are `cdf_<name>` fields with their own logic hooks. See `references/EXTENSIONS_INDEX.md`.

Authoritative details always live in the reference pages; do not rely on this summary alone.

## Common tasks

| Task | Start at |
|---|---|
| Signature/usage of any bshell function | `references/FUNCTION_INDEX.md` |
| Which 4GL section/subsection exists | `guide/progguide/4gl_features/` |
| Write DAL hooks | `guide/progguide/functions_dal/overview.md` |
| File/dir I/O | `guide/progguide/functions_directory_file_operations/` |
| Dynamic SQL | `guide/progguide/functions_dynamic_sql_queries/` + `functions_sql_query_extensions/` |
| Baan SQL syntax (SELECT etc.) | `sql/progguide/functions_database_handling/select_statement.md` |
| Decode SQLSTATE error | `sql/progguide/sql_states_and_messages/<code>.md` |
| String/date/format functions | `functions_string_operations/`, `functions_date_time_zones/`, `functions_formatting_io/` |
| Add a hook to a standard table/session | `references/extensions/table_extension_point.md`, `extensions/session_extension_point.md` |
| CDF types, config, limitations | `references/extensions/customer_defined_fields.md` |
| Extension Modeler workflow / activation | `references/extensions/extension_modeler.md` |
| Extend BOD/BDE UserArea (macros) | `references/extensions/bod_bde_extension_point.md` |
| Debug an extension | `references/extensions/extension_debugging.md` |
| Cloud restrictions / governors / best practices | `references/extensions/governance.md` |
| Export/import extensions (deployment) | `references/extensions/extension_deployment.md` |

## Notes

- Sources: Infor progguide 10.8.12pre (en) + Infor LN Extensions Development Guide 10.8 (01062026). Content is verbatim from the official guides.
- All files UTF-8 Markdown; code examples fenced; tables preserved.
- `search.py` needs only Python 3 stdlib; safe on Windows/Linux/macOS.
