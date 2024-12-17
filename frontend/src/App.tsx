import "./App.css";
import {ClickCounter} from "./components/ClickCounter";
import {Chat} from "./components/Chat";

function App() {
  return (
    <div className="App">
      <h1>Projekt PIS 2024Z</h1>
      <p>Profile: {process.env.NODE_ENV}</p>
      <p>Hello world</p>
      <Chat/>
      {/*TODO: API call*/}
    </div>
  );
}

export default App;
