import React, { useState, useEffect } from "react";
import {
  get_event_1_seq,
  get_latest_request_form,
  get_form_stats
} from "../scripts/serviceRequests";

export default function UiComponent(props) {
  
  const [readings, setReadings] = useState("readings");

  const getData = async () => {
    const dataObj = {};

    var latestForm = {};
    var formStats = {};
    await get_latest_request_form().then(result => {
      latestForm = result.payload;
    });

    await get_form_stats().then(result => {
      formStats = result;
    });
    // console.log(latestForm)
    dataObj["NumOfOrders"] = formStats.num_orders;
    dataObj["NumOfRepair"] = formStats.num_repair;
    dataObj["LastCustomer"] = latestForm.customer_id;
    dataObj["LastUpdated"] = Date();

    setReadings(dataObj);
  };

  useEffect(() => {
    setTimeout(getData, 2000);
  }, [readings]);

  return (
    <div className="UiComponent">
      <header className="App-header">
      <h1>Shoe orders and repair forms</h1>
        <div>
        <p>Number of orders: {readings.NumOfOrders}</p>
        <p>Number of repair requests: {readings.NumOfRepair}</p>
        <p>Last Customer: {readings.LastCustomer}</p>
        <p>Last Updated: {readings.LastUpdated}</p>

        </div>

      </header>
    </div>
  );
}
