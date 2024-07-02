import os
import requests
from typing import Literal, List, Optional
from datetime import datetime
import duckdb
import io
import contextlib
from blueprints.function_calling_blueprint import Pipeline as FunctionCallingBlueprint


class Pipeline(FunctionCallingBlueprint):
    class Valves(FunctionCallingBlueprint.Valves):
        # Add your custom parameters here
        MIMIC_DUCKDB_PATH: str = ""
        pass

    class Tools:
        def __init__(self, pipeline) -> None:
            self.pipeline = pipeline

        def get_table_schema(self,
                             table_name: str
                             ) -> str:
            """
            Get the schema of a specific table.

            :param table_name: The name of the table.
            :return: String containing the table schema in JSON format.
            """
            query = f"DESCRIBE {table_name};"

            print(f"------_GETTING TABLE SCHEMA______________________ {query}")
            if not self.pipeline.valves.MIMIC_DUCKDB_PATH:
                return "MIMIC Database Path is not set, ask the user to set it up."

            connection = duckdb.connect(
                database=self.pipeline.valves.MIMIC_DUCKDB_PATH,
                read_only=True,
            )
            result = connection.execute(query).fetchdf()
            return result.to_json(orient="records")

        def execute_query(self,
                          query: str
                          ) -> str:
            """
            Execute a custom query and return the result as a JSON string.
            Validate the query against the database schema and handle exceptions.

            :param query: The SQL query to execute.
            :return: String containing the query result in JSON format.
            :raises: ValueError if the query is invalid or if there is a schema mismatch.
            """
            print("------_EXECUTING QUERY______________________")
            try:
                connection = duckdb.connect(
                    database=self.pipeline.valves.MIMIC_DUCKDB_PATH,
                    read_only=True,
                )
                df = connection.execute(query).fetchdf()
                return df.to_json(orient="records")
            except Exception as e:
                raise e

        def get_current_time(
                self,
        ) -> str:
            """
            Get the current time.

            :return: The current time.
            """

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return f"Current Time = {current_time}"

        def get_owner_name(
                self,
        ) -> str:
            """
            Get the owner name

            :return: The current time in EST.
            """
            print("------_GETTING CURRENT TIME______________________")
            return f"Owner Name = ABC aka Abhishek Choudhary'"

        def show_tables(
                self,
        ) -> str:
            """
            Show all tables and schemas available in the MIMIC-IV database.

            :return: String containing table and schema information in JSON format.
            """
            print("------_SHOWING TABLES______________________")
            query = "SELECT * FROM information_schema.tables;"
            connection = duckdb.connect(
                    database=self.pipeline.valves.MIMIC_DUCKDB_PATH,
                    read_only=True,
                )
            result = connection.execute(query).fetchdf()
            return result.to_json(orient="records")

        def execute_code(self, code: str) -> str:
            """
            Execute a Python code and return the output.

            :param code: The Python code to execute.
            :return: The output of the code execution.
            """
            print("------_EXECUTING CODE______________________")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                try:
                    exec(code)
                except Exception as e:
                    return f"Error executing code: {e}"

            return output.getvalue()



    def __init__(self):
        super().__init__()
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "my_tools_pipeline"
        self.name = "My Tools Pipeline"
        self.valves = self.Valves(
            **{
                **self.valves.model_dump(),
                "pipelines": ["*"],  # Connect to all pipelines
                "MIMIC_DUCKDB_PATH": os.getenv("MIMIC_DUCKDB_PATH", ""),
            },
        )
        self.tools = self.Tools(self)
