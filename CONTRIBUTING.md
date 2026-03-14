# Contributing to Clarity Mirror

Thank you for your interest in helping people see their data clearly.

## Getting Started

1. Fork the repository and clone your fork
2. Open `app/clarity-mirror.html` in a browser to see the current prototype
3. Browse open [Issues](../../issues) to find something to work on
4. Comment on the issue to let others know you're working on it

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test locally
4. Submit a pull request with a clear description

## Areas Where We Need Help

### Privacy & Legal Engineering
- Researching data broker access mechanisms
- Writing CCPA/GDPR request templates
- Documenting broker response formats
- Tracking changes in privacy regulations

### Data Engineering
- Building parsers for broker response formats (PDF, CSV, XML, JSON)
- Mapping broker-specific attributes to the unified schema
- Writing tests for normalization edge cases

### Platform Integration
- Google Takeout ad profile parsing
- Meta data export parsing
- Amazon/TikTok/other platform export parsing

### ML & Federated Learning
- Implementing FedAvg with Flower
- Differential privacy integration
- Reflection effectiveness modeling

### UX & Content Design
- Translating broker category codes into human-readable vulnerability descriptions
- Writing mindful reflection prompts
- User testing and feedback

### Security
- Threat modeling for local data storage
- Identity verification flow design
- Reviewing the federated learning privacy model

## Guidelines

- **Privacy first**: Never commit personal data, API keys, or broker responses to the repo
- **Local-first**: All features should work offline by default
- **Calm design**: Language should promote awareness, not anxiety
- **Test your changes**: Include tests for any data parsing or analysis logic
- **Document your work**: Update relevant docs in the `docs/` directory

## Questions?

Open a Discussion thread — we're happy to help you find the right place to contribute.
