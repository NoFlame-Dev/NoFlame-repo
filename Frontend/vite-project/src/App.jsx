import { useState, useEffect } from "react";
import "./App.css";
import Fire from "./Fire";
import { GoogleMap, useJsApiLoader, Marker } from "@react-google-maps/api";
import { getCurrentForecast, getFireRisk, getCityName } from "./Api.jsx";

function App() {
  const [firePercentage, setFirePercentage] = useState(0);
  const [currentLocation, setCurrentLocation] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [fireRisk, setFireRisk] = useState(null); // Store fire risk
  const [isLoading, setIsLoading] = useState(true);
  const [cityName, setCityName] = useState("Fetching...");

  // Load Google Maps API
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: "AIzaSyAClGQYQDrnLDd8xxq0-9NIZGtaktlsqb4", // Replace with your actual API key
  });

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          setCurrentLocation({ lat: latitude, lng: longitude });
          
          try {
            const weather = await getCurrentForecast(latitude, longitude);
            const risk = await getFireRisk(latitude, longitude);
            const city = await getCityName(latitude, longitude);
            setWeatherData(weather);
            setFireRisk(risk);
            setCityName(city);
          } catch (error) {
            console.error("Error fetching data:", error);
          } finally {
            setIsLoading(false);
          }
        },
        (error) => {
          console.error("Error fetching location:", error);
          setIsLoading(false);
        }
      );
    } else {
      console.error("Geolocation is not supported by this browser.");
      setIsWeatherLoading(false);
    }
  }, []);

  // Map container style
  const mapContainerStyle = {
    width: "100%",
    height: "100%",
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>DASHBOARD</h1>
      </header>

      <div className="boxes">
        <div className="left-column">
          <div className="rounded-box weather-box">
            {isLoading ? (
            <p> Loading weather...</p>
          ) : weatherData ? (
            <>
              <p className="location">{cityName}</p>
              <p className="temperature">{weatherData.temperature}°</p>
            </>
          ) : (
            <p>Unable to fetch weather</p>
          )}
          </div>
          <div className="rounded-box humidity-box">
            {isLoading ? (
              <p> Loading humidity...</p>
            ) : weatherData && weatherData.relativeHumidity ? (
              <>
                <p className="humidity-title">Humidity</p>
                <p className="humidity-value">{weatherData.relativeHumidity}%</p>
              </>
            ) : (
              <p>Unable to fetch humidity data</p>
            )}
          </div>
          <div className="rounded-box">Wind Speed</div>
          <div className="rounded-box">Positive</div>
        </div>

        <div className="center-column">
          <div className="fire-percentage">
            { fireRisk !== null && (
              <>
                <div className="percentage-text">
                  Risk Factor:
                </div> 
                <p className="risk-value">{fireRisk}</p>
              </> 
            )}
            {fireRisk !== null && fireRisk > 0 && (
              <div
                className="fire-container"
                style={{
                  transform: `scale(${fireRisk / 100})`,
                }}
              >
                <Fire />
              </div>
            )}
          </div>
            <div className="safety-list">
              <ul>
              <ul className="safety-title"><strong>Safety checklist</strong></ul>
              <li><strong>Water (1 gallon per person/day)</strong></li>
              <li>Non-perishable food</li>
              <li>Medications and first aid supplies</li>
              <li>Flashlights, batteries, and phone chargers</li>
              <li><strong>Important documents (stored in a waterproof bag)</strong></li>
              <li>AN95 Masks or Respirators</li>
              <li><strong>Emergency Blanket or Sleeping Bags</strong></li>
              <li>Portable Radio</li>
              <li>Clothing and Sturdy Shoes</li>
              <li>Evacuation Plan and Map</li>
              </ul>
            </div>
          </div>

        <div className="right-column">
        <div
  className="fire-likely"
  style={{
    background: fireRisk <= 25
      ? 'linear-gradient(135deg, green, yellow)'  
      : fireRisk <= 50
      ? 'linear-gradient(135deg, yellow, orange)'
      : fireRisk <= 75
      ? 'linear-gradient(135deg, orange 20%, red 80%)' 
      : 'linear-gradient(135deg, red 50%, darkred 100%)',      
    transition: "background 0.5s ease", 
  }}
>
  Likelihood of fire
</div>



          <div className="map">
            {isLoaded && currentLocation ? (
              <GoogleMap
                mapContainerStyle={mapContainerStyle}
                center={currentLocation}
                zoom={15}
              >
                {/* Marker to indicate user's current location */}
                <Marker position={currentLocation} />
              </GoogleMap>
            ) : (
              <p>Loading map...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
