#!/usr/bin/env python3
"""
API Smoke Test Script for Diabetes Prediction Service.
Uses Python standard library (urllib) to test API endpoints against a target base URL.
Usage:
    python test_api.py [--base-url http://127.0.0.1:8000]
"""

import sys
import json
import argparse
import urllib.request
import urllib.error

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    
    encoded_data = None
    if data is not None:
        if isinstance(data, dict) or isinstance(data, list):
            encoded_data = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif isinstance(data, str):
            encoded_data = data.encode("utf-8")
            headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body_bytes = response.read()
            try:
                body = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                body = body_bytes.decode("utf-8")
            return status, body
    except urllib.error.HTTPError as e:
        body_bytes = e.read()
        try:
            body = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            body = body_bytes.decode("utf-8")
        return e.code, body
    except Exception as e:
        return None, str(e)

def run_tests(base_url):
    base_url = base_url.rstrip("/")
    passed = 0
    failed = 0

    print(f"🚀 Running API Smoke Tests against {base_url}\n" + "=" * 60)

    def report_test(name, is_success, details):
        nonlocal passed, failed
        if is_success:
            passed += 1
            print(f"✅ PASS: {name}")
            print(f"   Details: {details}\n")
        else:
            failed += 1
            print(f"❌ FAIL: {name}")
            print(f"   Details: {details}\n")

    # Test 1: GET /
    status, body = make_request(f"{base_url}/")
    expected_msg = {"message": "Diabetes Prediction API is live"}
    report_test("GET / Root Endpoint", status == 200 and body == expected_msg, f"Status={status}, Body={body}")

    # Test 2: GET /docs
    status, body = make_request(f"{base_url}/docs")
    report_test("GET /docs Documentation", status == 200, f"Status={status}")

    # Test 3: GET /openapi.json
    status, body = make_request(f"{base_url}/openapi.json")
    has_predict = isinstance(body, dict) and "/predict" in body.get("paths", {})
    report_test("GET /openapi.json Schema", status == 200 and has_predict, f"Status={status}, Contains /predict={has_predict}")

    # Test 4: POST /predict (Fixed Sample)
    fixed_sample = {
        "Pregnancies": 2,
        "Glucose": 130,
        "BloodPressure": 70,
        "BMI": 28.5,
        "Age": 45
    }
    status, body = make_request(f"{base_url}/predict", method="POST", data=fixed_sample)
    expected_pred = {"diabetic": True}
    report_test("POST /predict Fixed Sample", status == 200 and body == expected_pred, f"Status={status}, Body={body}")

    # Test 5: POST /predict (Repeatability Check)
    status2, body2 = make_request(f"{base_url}/predict", method="POST", data=fixed_sample)
    report_test("POST /predict Repeatability", status2 == 200 and body2 == expected_pred, f"Status={status2}, Body={body2}")

    # Test 6: POST /predict (Non-Diabetic Sample)
    nondiabetic_sample = {
        "Pregnancies": 0,
        "Glucose": 85,
        "BloodPressure": 66,
        "BMI": 22.0,
        "Age": 22
    }
    status_nd, body_nd = make_request(f"{base_url}/predict", method="POST", data=nondiabetic_sample)
    expected_nd = {"diabetic": False}
    report_test("POST /predict Non-Diabetic Sample", status_nd == 200 and body_nd == expected_nd, f"Status={status_nd}, Body={body_nd}")

    # Test 7: Invalid Case - Empty Object
    status_empty, body_empty = make_request(f"{base_url}/predict", method="POST", data={})
    report_test("Invalid POST /predict Empty JSON", status_empty == 422, f"Status={status_empty} (Expected 422)")

    # Test 8: Invalid Case - Missing Field
    missing_sample = {
        "Pregnancies": 2,
        "BloodPressure": 70,
        "BMI": 28.5,
        "Age": 45
    }
    status_missing, body_missing = make_request(f"{base_url}/predict", method="POST", data=missing_sample)
    report_test("Invalid POST /predict Missing Field", status_missing == 422, f"Status={status_missing} (Expected 422)")

    # Test 9: Invalid Case - Nonnumeric String
    nonnumeric_sample = {
        "Pregnancies": 2,
        "Glucose": "not-a-number",
        "BloodPressure": 70,
        "BMI": 28.5,
        "Age": 45
    }
    status_nonnum, body_nonnum = make_request(f"{base_url}/predict", method="POST", data=nonnumeric_sample)
    report_test("Invalid POST /predict Non-numeric String", status_nonnum == 422, f"Status={status_nonnum} (Expected 422)")

    # Test 10: Invalid Case - Null Value
    null_sample = {
        "Pregnancies": 2,
        "Glucose": None,
        "BloodPressure": 70,
        "BMI": 28.5,
        "Age": 45
    }
    status_null, body_null = make_request(f"{base_url}/predict", method="POST", data=null_sample)
    report_test("Invalid POST /predict Null Field", status_null == 422, f"Status={status_null} (Expected 422)")

    # Test 11: Invalid Case - Malformed JSON
    malformed_raw = '{"Pregnancies": 2,'
    status_malformed, body_malformed = make_request(f"{base_url}/predict", method="POST", data=malformed_raw)
    report_test("Invalid POST /predict Malformed JSON Syntax", status_malformed == 422, f"Status={status_malformed} (Expected 422, Body error='{body_malformed.get('detail', [{}])[0].get('msg') if isinstance(body_malformed, dict) else body_malformed}')")

    print("=" * 60)
    print(f"📊 Smoke Test Summary: Total={passed + failed}, Passed={passed}, Failed={failed}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="API Smoke Tests")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Base URL of the API")
    args = parser.parse_args()

    sys.exit(run_tests(args.base_url))
