# Daily AI Post Pipeline

An automated system that generates AI-powered content about specified topics and stores them in a Supabase database. Runs daily via GitHub Actions.

Just a test that I need to check

Adding additional text only in caps 

## 🌟 Features

- **Modular Design**: Clean, maintainable code structure
- **Flexible Query System**: Easily modify search topics via `query.txt`
- **AI-Powered Content**: Uses Google's Gemini 2.0 Flash model
- **Automated Scheduling**: Daily execution via GitHub Actions (7 AM IST)
- **Database Storage**: Structured data storage in Supabase
- **Dual Configuration**: Environment variables (production) + config.json (local)
- **🔒 Security**: API keys protected and not exposed in repository

## 📁 Project Structure

```
post_pipeline/
├── main.py                    # Main pipeline script
├── query.txt                  # Search query (easily editable)
├── prompt_template.txt        # AI prompt template
├── requirements.txt           # Python dependencies
├── config.json.example        # Configuration template (copy to config.json)
├── env.example               # Environment template (copy to .env)
├── .gitignore               # Git ignore rules
├── .github/
│   └── workflows/
│       └── daily-post.yml   # GitHub Actions workflow
└── README.md                # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anushanuka/post_pipeline.git
   cd post_pipeline
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials** (choose one):
   
   **Option A: Using .env file**
   ```bash
   # Copy the example file and add your credentials
   cp env.example .env
   # Edit .env with your actual API keys
   ```
   
   **Option B: Using config.json**
   ```bash
   # Copy the example file and add your credentials
   cp config.json.example config.json
   # Edit config.json with your actual API keys
   ```

4. **Customize your query**:
   Edit `query.txt` with your desired search topic:
   ```
   AI Agents using LangGraph in the last 1 day
   ```

5. **Run the pipeline**:
   ```bash
   python main.py
   ```

### GitHub Actions Setup

1. **Set Repository Secrets**:
   Go to your GitHub repository → Settings → Secrets and variables → Actions
   
   Add these secrets:
   - `GEMINI_API_KEY`: Your Google AI API key
   - `SUPABASE_PROJECT_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase service role key

2. **Enable Actions**: 
   The workflow will run automatically daily at 7 AM IST, or you can trigger it manually.

## 🔧 Configuration

### Supabase Database Schema

Create a table named `post_pipeline` with:
```sql
CREATE TABLE post_pipeline (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  post JSONB NOT NULL,
  source TEXT NOT NULL
);
```

### Customization

- **Change Query**: Edit `query.txt`
- **Modify Prompt**: Edit `prompt_template.txt`
- **Adjust Schedule**: Modify the cron expression in `.github/workflows/daily-post.yml`
- **Update Dependencies**: Modify `requirements.txt`

## 🔒 Security

- **API Keys Protected**: Both `config.json` and `.env` are ignored by git and won't be pushed to repository
- **Use Example Files**: Copy `config.json.example` to `config.json` or `env.example` to `.env` for local development
- **GitHub Secrets**: Production uses encrypted repository secrets
- **No Key Exposure**: Your sensitive credentials remain private and secure

## 📊 Data Structure

The generated content is stored as JSON with this structure:
```json
{
  "query": "AI Agents using LangGraph in the last 1 day",
  "generated_at": "2024-01-15T12:00:00.000Z",
  "model": "gemini-2.0-flash-exp",
  "content": "Generated AI content...",
  "search_date_range": "2024-01-14 to 2024-01-15",
  "prompt_version": "template_v1"
}
```

## 🛠️ Development

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `python main.py`
5. Submit a pull request

### Troubleshooting

- **API Errors**: Check your API keys and quotas
- **Database Errors**: Verify Supabase URL and permissions
- **Workflow Failures**: Check GitHub Actions logs and secrets
- **Missing config files**: Copy from `config.json.example` or `env.example` and add your keys

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
