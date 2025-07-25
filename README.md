# Cloud Cost Optimizer

Cloud Cost Optimizer is a lightweight toolset designed to help DevOps and Cloud Engineers estimate and compare infrastructure costs across major cloud providers. The current version supports comparisons between AWS and GCP based on instance types, storage, networking, and optional managed services.

## Features

- Cost estimation for common infrastructure components
- Comparison between AWS and GCP pricing
- Simple JSON or YAML input format
- Optimization suggestions for reducing cloud costs
- Modular design for easy extension

## Use Cases

- Migration planning from AWS to GCP or vice versa
- Budget forecasting and validation
- Infrastructure cost audits
- Educational purposes for understanding cost trade-offs

## Technologies

- Python 3.x
- Public pricing APIs and official pricing sheets (where available)
- Pandas for data processing
- Jinja2 (for generating reports, optional)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `pip install -r requirements.txt`

### Example

```
python main.py --input configs/example-infra.yaml --output report.html
```

## File Structure

```
cloud-cost-optimizer/
├── configs/
│   └── example-infra.yaml
├── data/
│   └── cached_pricing/
├── src/
│   ├── aws.py
│   ├── gcp.py
│   ├── optimizer.py
│   └── report_generator.py
├── tests/
│   └── test_optimizer.py
├── requirements.txt
└── README.md

```

## Roadmap

 - Add support for Azure
 - Include carbon footprint estimation
 - Add Terraform state file parser (experimental)
 - Export reports as PDF

## License
MIT License




