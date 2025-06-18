# Base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y openjdk-17-jre wget unzip ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install OWASP ZAP
RUN wget \
  https://github.com/zaproxy/zaproxy/releases/download/v2.16.1/ZAP_2.16.1_Linux.tar.gz \
  -O /tmp/zap.tar.gz && \
  tar -xzf /tmp/zap.tar.gz -C /opt && \
  rm /tmp/zap.tar.gz



# Add ZAP to PATH
ENV PATH="/opt/ZAP_2.16.1:${PATH}"

# Add a default scan script (optional, for baseline scan)
COPY zap-scan.sh /zap-scan.sh
RUN chmod +x /zap-scan.sh

# Set entrypoint (optional)
# ENTRYPOINT ["/zap-baseline-scan.sh"]

# For running tests manually
CMD ["bash"]
