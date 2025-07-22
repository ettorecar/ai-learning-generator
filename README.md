# AI-Powered E-Learning Course & Quiz Generator

An intelligent web platform that leverages **Generative AI** to create personalized educational content and interactive quizzes in seconds. Transform any topic into a comprehensive learning experience with AI-generated courses, custom assessments, and multilingual support.

## 🚀 Key Features

### 🤖 **Generative AI Integration**
- **OpenAI GPT Integration**: Powered by OpenAI's advanced language models for content generation
- **AI Image Generation**: Automatic topic-relevant image creation using DALL-E
- **Smart Content Creation**: Generates comprehensive course summaries (~500 words) with contextual accuracy
- **Intelligent Quiz Generation**: Creates relevant questions with plausible distractors

### 📚 **Multi-Source Learning**
- **Topic-Based Generation**: Enter any subject and get instant course content
- **Article Processing**: Paste existing articles for quiz generation
- **URL Content Extraction**: Extract and process content from web URLs
- **Random Topic Discovery**: AI suggests and creates content for random educational topics

### 🌍 **Multilingual Support**
- **4 Languages Available**: Italian, English, French, and Spanish
- **Localized Interface**: Complete UI translation for all supported languages
- **Content Generation**: AI generates course materials in the selected language

### 📝 **Customizable Assessment**
- **Flexible Quiz Configuration**:
  - Custom number of questions (1-N)
  - Variable answer options per question (2-N)
  - Single-answer or multiple-choice formats
  - Adjustable passing threshold (1-100%)
- **Real-time Preview**: Interactive quiz preview before generation
- **Instant Scoring**: Automated grading with detailed feedback

### 🎨 **Modern Web Interface**
- **Responsive Design**: Bootstrap-based responsive layout
- **Interactive UI**: Dynamic form validation and real-time updates
- **Visual Feedback**: Loading animations and progress indicators
- **Professional Styling**: Modern CSS with Font Awesome icons

## 🛠 Technology Stack

### **Backend**
- **Python Flask**: RESTful API server
- **OpenAI API**: GPT models for text generation and DALL-E for images
- **Flask-CORS**: Cross-origin resource sharing support

### **Frontend**
- **HTML5/CSS3**: Modern semantic markup and styling
- **JavaScript ES6**: Modular JavaScript with import/export
- **Bootstrap 5**: Responsive grid system and components
- **jQuery**: DOM manipulation and AJAX requests

### **Styling & Assets**
- **Font Awesome**: Professional icon library
- **Custom CSS**: Branded styling and animations
- **Web Fonts**: Poppins font family for modern typography

## 📋 User Input Parameters

### **Content Source Selection** (Required - Choose One)
1. **Topic**: Free text input for any subject area
2. **Article**: Paste existing article content
3. **URL**: Provide web link for content extraction
4. **Random Topic**: Let AI choose a random educational topic

### **Quiz Configuration** (Required)
- **Number of Questions**: Integer input (recommended: 1-20)
- **Number of Answer Options**: Integer input (recommended: 2-5)
- **Answer Type**: 
  - Single Answer (radio buttons)
  - Multiple Choice (checkboxes)
- **Passing Threshold**: Percentage slider (1-100%)
- **Language**: Dropdown selection (Italian/English/French/Spanish)

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- OpenAI API key
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ettorecar/ai-learning-generator.git
cd ai-learning-generator
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure OpenAI API**
```python
# Update openai_mw.py with your API key
openai.api_key = 'your-openai-api-key-here'
```

4. **Start the Flask server**
```bash
python openai_mw.py
```

5. **Launch the web interface**
```bash
# Open index.html in your web browser
# Or serve with a local web server on port 5500
```

## 🔧 Configuration

### API Endpoint Configuration
The application expects the Flask API to run on `http://127.0.0.1:8080` by default. Update the endpoint in `quiz.js` if needed:

```javascript
fetch('http://your-api-endpoint/api/v.1.0/middleware_chatgpt', requestOptions)
```

### CORS Configuration
The Flask server is configured to accept requests from `http://127.0.0.1:5500`. Update the CORS settings in `openai_mw.py` for different origins:

```python
CORS(app, resources={r"/*": {"origins": "http://your-frontend-url"}})
```

## 📁 Project Structure

```
├── index.html              # Main landing page and quiz configuration
├── quiz.html              # Quiz display and interaction page
├── openai_mw.py           # Flask API server with OpenAI integration
├── quiz.js                # Quiz logic and API communication
├── constants.js           # Multilingual constants and translations
├── requirements.txt       # Python dependencies
├── css/                   # Stylesheets and frameworks
│   ├── bootstrap.min.css  # Bootstrap framework
│   ├── style.css         # Custom styles
│   └── index.css         # Page-specific styles
├── js/                    # JavaScript libraries
│   ├── jquery.min.js     # jQuery library
│   └── custom.js         # Custom interactions
├── images/                # Static assets and generated images
└── fonts/                 # Web fonts and icon fonts
```

## 🎯 Use Cases

### **Educational Institutions**
- Rapid course material development
- Automated assessment creation
- Multilingual educational content
- Student self-assessment tools

### **Corporate Training**
- Employee skill assessment
- Training material generation
- Compliance testing
- Onboarding quizzes

### **Content Creators**
- Educational content generation
- Blog post quizzes
- Learning verification tools
- Audience engagement

### **Self-Learners**
- Topic exploration
- Knowledge testing
- Study material creation
- Progress tracking

## 🔒 Security Considerations

- **API Key Protection**: Store OpenAI API keys securely (environment variables recommended)
- **Input Validation**: Implement proper validation for user inputs
- **Rate Limiting**: Consider implementing rate limiting for API calls
- **CORS Policy**: Configure appropriate CORS policies for production

## 🚀 Future Enhancements

- **User Authentication**: Login system for personalized learning
- **Progress Tracking**: Learning analytics and progress monitoring
- **Advanced AI Features**: Integration with newer OpenAI models
- **Export Capabilities**: PDF/SCORM export for generated content
- **Database Integration**: Persistent storage for courses and results
- **Mobile App**: Native mobile applications
- **Collaborative Features**: Course sharing and collaboration tools

## �‍💻 Authors

- **[Ettore Carpinella]** - *Project Creator & Lead Developer*
- **[Maria Rosaria Lorito, Raffaella Tuozzolo]** - *Senior developer*

## �📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

For support, questions, or feature requests, please open an issue on GitHub or contact the development team at [ettorecar.git  at gmail ]

---

**Powered by OpenAI GPT & DALL-E | Built with ❤️ for Educational Innovation**
