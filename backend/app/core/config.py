from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la app.

    Cada atributo se puede sobrescribir con una variable de entorno del mismo
    nombre (DATABASE_URL, CORS_ORIGINS) o desde un archivo .env, sin tocar código.
    """

    database_url: str = "sqlite:///./flowtask.db"
    # Orígenes a los que el navegador tiene permitido llamar a la API (CORS estricto).
    cors_origins: list[str] = ["http://localhost:4200"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
