import string
import requests
from sylphid_core import errors as syl_errors
from sylphid_core.asset_management import util


class Client:
    def __init__(self, url):
        self.url = url

    def add_products(self, data, fields):
        return self._mutate("addProduct", "addProduct", data, "product", fields)

    def add_workfiles(self, data, fields):
        return self._mutate("addWorkfile", "addWorkfile", data, "workfile", fields)

    def add_workarea(self, data, fields):
        return self._mutate("addWorkarea", "addWorkarea", data, "workarea", fields)

    def _mutate(self, name, method, input_data, type_, fields):
        mutation = util.generate_mutation(
            name, method, input_data, type_, fields
        )

        response = requests.post(
            self.url,
            json={
                "query": mutation
            }
        )

        if response.status_code == 200:
            data = response.json()
            errors = data.get("errors")

            # TODO: Log properly
            if errors:
                for error in errors:
                    print(error)
                raise syl_errors.AssetManagementError("Mutation Error, Please see log.")

            return data["data"][name][type_]

        else:
            raise syl_errors.AssetManagementError(
                "HTTP Error: code: {}".format(response.status_code)
            )
