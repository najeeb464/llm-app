import axios from "axios";

const api = axios.create({
  baseURL: "" 
});

export const fetchAnalytics = () =>
  api.get("/analytics").then((r) => r.data);

export const fetchTraces = (category = "") =>
  api
    .get("/traces", { params: category ? { category } : {} })
    .then((r) => r.data);


  export const sendChat = (message) =>
  api.post("/chat", { message }).then((r) => r.data);
  fetchAnalytics();
  fetchTraces();
