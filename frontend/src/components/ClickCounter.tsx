import {useState} from "react";
import styles from "./ClickCounter.module.css";

export const ClickCounter = () => {
    const [count, setCount] = useState(0);

    return (
        <div className={styles.wrapper}>
            <p>You clicked {count} times</p>
            <button onClick={() => setCount(count + 1)}>Click me</button>
        </div>
    );
};