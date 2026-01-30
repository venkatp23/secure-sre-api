variable "gemini_api_key" {
  description = "API Key for Google Gemini AI"
  type        = string
  sensitive   = true # This prevents the key from being printed in your terminal logs
}

variable "github_token" {
  description = "Personal Access Token for GitHub"
  type        = string
  sensitive   = true # This hides your token from the terminal logs
}

variable "github_owner" {
  description = "The GitHub username or organization name"
  type        = string
}