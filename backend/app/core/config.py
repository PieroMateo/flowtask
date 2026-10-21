from pydantic_settings import BaseSettings, SettingsConfigDict


# si existe una variable de entorno con el mismo nombre (DATABASE_URL, CORS_ORIGINS)
# se usa esa en lugar del valor de aqui, asi docker cambia la config sin tocar codigo
class Settings(BaseSettings):
    database_url: str = "sqlite:///./flowtask.db"
    # origenes que pueden llamar a la API desde el navegador
    cors_origins: list[str] = ["http://localhost:4200"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
