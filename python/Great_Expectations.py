#Import library yang akan digunakan
from ruamel.yaml import YAML

import great_expectations as ge
from great_expectations.core.batch import BatchRequest
from great_expectations.core.expectation_configuration import ExpectationConfiguration

#Inisialisasi DataContext
context = ge.get_context()
datasource_config = {
    "name": "tweet-check",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SqlAlchemyExecutionEngine",
        "connection_string": "sqlite:///Tweets.db",
    },
    "data_connectors": {
        "default_runtime_data_connector_name": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["default_identifier_name"],
        },
        "default_inferred_data_connector_name": {
            "class_name": "InferredAssetSqlDataConnector",
            "name": "tweet",
        },
    },
}

# Menguji confignya. Akan mengeluarkan error jika salah
# context.test_yaml_config(yaml.dump(datasource_config))

#Menambahkan DataSource ke DataContext
context.add_datasource(**datasource_config)

# Membuat BatchRequest yang merujuk ke tabel
batch_request = BatchRequest(
    datasource_name="tweet-check",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="tweet",  # Nama tabel yang ingin diambil
)
suite = context.create_expectation_suite(
    expectation_suite_name="test_suite", overwrite_existing=True
)

#Setup Expectations
expectation_configuration = ExpectationConfiguration(
    expectation_type="expect_column_values_to_be_of_type",
    kwargs={
        "column": "tweet",
        "type_": "TEXT"
    }
)
suite.add_expectation(expectation_configuration=expectation_configuration)

validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="test_suite")

# Simpan Expectations
print(context.get_expectation_suite(expectation_suite_name="test_suite"))
context.save_expectation_suite(expectation_suite=suite, expectation_suite_name="test_suite")

# Buat Checkpoints
yaml = YAML()
my_checkpoint_name = "tweet-checking"

yaml_config = f"""
name: {my_checkpoint_name}
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: "%Y%m%d-%H%M%S-tweet-check"
validations:
  - batch_request:
      datasource_name: tweet-check
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: tweet
      data_connector_query:
        index: -1
    expectation_suite_name: test_suite
"""

# Menguji confignya. Akan mengeluarkan error jika salah
# my_checkpoint = context.test_yaml_config(yaml_config=yaml_config)

# Tambah checkpoint ke DataContext
context.add_checkpoint(**yaml.load(yaml_config))

# Testing checkpoint dan membuat report
# context.run_checkpoint(checkpoint_name=my_checkpoint_name)
# context.open_data_docs()