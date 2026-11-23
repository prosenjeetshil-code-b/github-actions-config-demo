import os
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file if it exists.
    # override=False ensures that environment variables already set in the process
    # (e.g. by GitHub Actions or the system environment) take precedence over the .env file.
    load_dotenv(override=False)

    # 1. Non-sensitive configuration values
    app_env = os.getenv("APP_ENV")
    api_base_url = os.getenv("API_BASE_URL")
    log_level = os.getenv("LOG_LEVEL")

    # 2. Sensitive configuration values (credentials)
    api_token = os.getenv("API_TOKEN")
    database_password = os.getenv("DATABASE_PASSWORD")

    # Evaluate presence safely without exposing secret contents
    is_api_token_set = bool(api_token and api_token.strip())
    is_db_password_set = bool(database_password and database_password.strip())

    print("========================================")
    print("APPLICATION CONFIGURATION")
    print("========================================")
    print()
    print(f"Environment: {app_env if app_env is not None else '[NOT SET]'}")
    print(f"API Base URL: {api_base_url if api_base_url is not None else '[NOT SET]'}")
    print(f"Log Level: {log_level if log_level is not None else '[NOT SET]'}")
    print()
    print(f"API Token configured: {is_api_token_set}")
    print(f"Database password configured: {is_db_password_set}")
    print()
    print("========================================")

    # Informative check for missing configuration
    missing_items = []
    if app_env is None:
        missing_items.append("APP_ENV")
    if api_base_url is None:
        missing_items.append("API_BASE_URL")
    if log_level is None:
        missing_items.append("LOG_LEVEL")
    if not is_api_token_set:
        missing_items.append("API_TOKEN")
    if not is_db_password_set:
        missing_items.append("DATABASE_PASSWORD")

    if missing_items:
        print()
        print(f"[INFO] Unset or empty configuration keys: {', '.join(missing_items)}")


if __name__ == "__main__":
    main()
