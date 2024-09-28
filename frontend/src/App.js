import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';

function RunList() {
  const [runs, setRuns] = React.useState([]);

  React.useEffect(() => {
    axios.get('/api/runs')
      .then(response => setRuns(response.data))
      .catch(error => console.error('Error fetching runs:', error));

  }, []);

  return (
    <div>
      <h2>Recent Runs</h2>
      <ul>
        {runs.map(run => (
            <li key={run.id}>{new Date(run.date).toLocaleDateString()} - {run.distance} mi</li>
          ))}
      </ul>
    </div>
  );
}

function RecommendationForm() {
  const [recommendation, setRecommendation] = React.useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post('/api/recommend', {/* add form data here */})
      .then(response => setRecommendation(response.data.recommendation))
      .catch(error => console.error('Error getting recommendation:', error));
  };

  return (
    <div>
      <h2>Get Recommendation</h2>
      <form onSubmit={handleSubmit}>
        {/* add form fields here*/}
        <button type="submit">Get Recommendation</button>
      </form>
      {recommendation && <p>Recommendation: {recommendation}</p>}
    </div>
  );
}

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/recommend">Get Recommendation</Link></li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" exact component={RunList} />
          <Route path="/recommend" Component={RecommendationForm} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;