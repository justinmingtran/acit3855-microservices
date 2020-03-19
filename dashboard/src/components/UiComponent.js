import React, { useState, useEffect } from "react";
import { get_inventory_stats } from "../scripts/serviceRequests";

export default function UiComponent(props) {
  const [readings, setReadings] = useState("readings");

  const getData = async () => {
    const dataObj = {};

    var inventoryStats = {};

    await get_inventory_stats().then(result => {
      console.log(result);
      inventoryStats = result;
    });
    // console.log(latestForm)
    dataObj["NumOfOrders"] = inventoryStats.num_order;
    dataObj["NumOfItems"] = inventoryStats.num_item;
    dataObj["LastUpdated"] = Date();
    setReadings(dataObj);
  };

  useEffect(() => {
    setTimeout(getData, 2000);
  }, [readings]);

  return (
    <div className="UiComponent">
      <header className="App-header">
        <h1>Iventory Dashboard</h1>
        <h2>Items and Orders</h2>
        <div>
          <p>Number of Orders: {readings.NumOfOrders}</p>
          <p>Number of Items: {readings.NumOfItems}</p>
          <p>Last Updated: {readings.LastUpdated}</p>
        </div>
      </header>
    </div>
  );
}
