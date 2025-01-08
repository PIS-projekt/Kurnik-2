import "./App.css";
import {Chat} from "./components/Chat";

export const apiBaseUrl = "http://0.0.0.0:8000";

function App() {

  return (
    <div className="App">
      <h1>Projekt PIS 2024Z</h1>
      <p>Profile: {process.env.NODE_ENV}</p>
      <Chat/>
    </div>
  );
}

export default App;
