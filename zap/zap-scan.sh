#!/bin/bash

TARGET_URL=${1:-"http://localhost:8080"}
REPORT_FILE=${2:-"zap_report.html"}

echo "Running OWASP ZAP Baseline Scan on ${TARGET_URL}"

zap.sh -cmd -quickurl $TARGET_URL -quickout $REPORT_FILE -quickprogress
if [ $? -eq 0 ]; then
    echo "Scan completed successfully. Report saved to ${REPORT_FILE}"
else
    echo "Scan failed."
    exit 1
fi
# Check if the report file was created