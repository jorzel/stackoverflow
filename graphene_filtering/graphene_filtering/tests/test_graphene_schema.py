import json

from graphene_django.utils.testing import GraphQLTestCase

from graphene_filtering.graphql.types import schema
from graphene_filtering.tests.factories import (
    EventFactory,
    PhotographerFactory,
    PurchaseOrderFactory,
    PurchaseOrderProductFactory,
)


class QueryTest(GraphQLTestCase):
    def setUp(self):
        self.graphql_schema = schema

    GRAPHQL_SCHEMA = schema

    def test_hi_query(self):

        query = self.query(
            """
            query {
                hello
            }
            """
        )

        response = {"data": {"hello": "Hi!"}}

        content = json.loads(query.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(query)
        assert response == content

    def test_event_photographer(self):
        photographer = PhotographerFactory(name="maro")
        _ = EventFactory(photographer=photographer)

        query = self.query(
            """
            query {
                events(photographer_Name: "maro") {
                    edges {
                        node {
                            photographer {
                                name
                            }
                        }
                    }
                }
            }
            """
        )

        response = {
            "data": {
                "events": {"edges": [{"node": {"photographer": {"name": "maro"}}}]}
            }
        }

        content = json.loads(query.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(query)
        assert response == content

    def test_purchases(self):
        order1 = PurchaseOrderFactory()
        order2 = PurchaseOrderFactory()
        _ = PurchaseOrderProductFactory(order=order1, name="access1")
        _ = PurchaseOrderProductFactory(order=order2, name="xxx")

        query = self.query(
            """
                query {
                    purchases(first: 15, after: "", products_Name: "access") {
                        edges {
                            node {
                                products {
                                    edges {
                                        node {
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                """
        )

        response = {
            "data": {
                "purchases": {
                    "edges": [
                        {
                            "node": {
                                "products": {"edges": [{"node": {"name": "access1"}}]}
                            }
                        }
                    ]
                }
            }
        }

        content = json.loads(query.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(query)
        assert response == content
