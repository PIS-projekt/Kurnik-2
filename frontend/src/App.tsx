import "./App.css";
import {ClickCounter} from "./components/ClickCounter";

function App() {
  return (
    <div className="App">
      <h1>Projekt PIS 2024Z</h1>
      <p>Profile: {process.env.NODE_ENV}</p>
      <p>Hello world</p>
      <ClickCounter/>
      {/*TODO: API call*/}
    </div>
  );
}

export default App;
