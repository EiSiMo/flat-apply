# flat-apply

## Description

Finding an apartment in Berlin is notoriously difficult.
However, those with a [WBS](https://service.berlin.de/dienstleistung/120671/) (housing entitlement certificate) can access state-subsidized housing via 
[inberlinwohnen.de](https://www.inberlinwohnen.de/wohnungsfinder).
New listings appear daily, but there is no waiting list; applicants are selected at random.
Crucially, the number of applications per listing is capped, often causing ads to disappear within an hour.
This necessitates constant monitoring of the website.

flat-apply solves this problem by automating the application process.
It integrates with my [flat-alert](https://github.com/EiSiMo/flat-alert) project.
When the alerter or the user finds a new flat listing, flat-apply grabs it from Telegram and applies automatically.

In Berlin exist six public housing associations. This projects wants to implement the application process for all of them.
It does not cover Immoscout or other sites.

## Project Status

This project is currently in early development and primarily designed for personal use.
Customizing filters currently requires technical knowledge,
but user-friendly configuration options are planned for future updates. Contributions are welcome.

### Current housing provider implementation reliability

| provider        | implementation status                 |
|:----------------|:--------------------------------------|
| gewobag.de      | 🟢 working but needs field testing    |
| gesobau.de      | 🔴 not working yet                    |
| degewo.de       | 🟢 working but needs field testing    |
| howoge.de       | 🟢 working but needs field testing    |
| stadtundland.de | 🟢 working but needs field testing    |
| wbm.de          | 🟢 working but needs field testing    |

## Quickstart

Follow these steps to run the program on your machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/eisimo/flat-apply.git
    ```
    ```bash
    cd flat-apply
    ```

2.  **Configure the environment:**
    Create a `.env` file in the root directory. Refer to `.env.example` for the required variables.

3.  **Run the application:**
    ```bash
    docker compose up -d
    ```

## Related Projects

*   [flat-apply](https://github.com/EiSiMo/flat-apply): A tool currently in development to automate the application process for flats found by flat-alert.
