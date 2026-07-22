from django.test import TestCase


class CalculatorRouteTests(TestCase):
    routes = {
        "/tools/position-size-calculator/": "ps-lots",
        "/tools/drawdown-calculator/": "dd-recover",
        "/risk-reward-calculator/": "rr-ratio",
        "/pip-value-calculator/": "pv-out",
        "/tools/profit-calculator/": "pl-out",
        "/tools/compounding-calculator/": "cp-final",
    }

    def test_all_legacy_calculator_routes_render(self):
        for route, output_id in self.routes.items():
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'id="{output_id}"')
                self.assertContains(response, '"@type":"SoftwareApplication"')

    def test_calculators_load_shared_runtime_and_disclosure(self):
        response = self.client.get("/tools/position-size-calculator/")
        self.assertContains(response, "js/calculators.js")
        self.assertContains(response, "Verify values before trading")
