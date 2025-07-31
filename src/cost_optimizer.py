import yaml

# Mocked pricing data (per hour for compute, per GB/month for storage)
PRICING = {
    "aws": {
        "compute": {
            "t3.medium": 0.0416,
            "t3.large": 0.0832
        },
        "storage": {
            "gp2": 0.10
        }
    },
    "gcp": {
        "compute": {
            "e2-standard-2": 0.034,
            "e2-standard-4": 0.068
        },
        "storage": {
            "pd-standard": 0.09
        }
    }
}

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def estimate_cost(provider, config):
    pricing = PRICING[provider]
    total = 0.0

    for instance in config.get("compute", []):
        instance_type = instance["type"]
        count = instance["count"]
        price = pricing["compute"].get(instance_type, 0)
        monthly = price * 24 * 30
        total += monthly * count

    for volume in config.get("storage", []):
        storage_type = volume["type"]
        size_gb = volume["size_gb"]
        price = pricing["storage"].get(storage_type, 0)
        total += price * size_gb

    return round(total, 2)

def main():
    config = load_config("configs/example-infra.yaml")

    aws_cost = estimate_cost("aws", config)
    gcp_cost = estimate_cost("gcp", config)

    print("=== Cloud Cost Estimation ===\n")
    print(f"Provider: AWS -> ${aws_cost}/month")
    print(f"Provider: GCP -> ${gcp_cost}/month\n")

    if aws_cost < gcp_cost:
        print(f"Suggested Provider: AWS (savings: ${round(gcp_cost - aws_cost, 2)})")
    elif gcp_cost < aws_cost:
        print(f"Suggested Provider: GCP (savings: ${round(aws_cost - gcp_cost, 2)})")
    else:
        print("Both providers have the same estimated cost.")

if __name__ == "__main__":
    main()
