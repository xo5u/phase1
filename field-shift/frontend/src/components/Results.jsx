import { useState } from 'react'
import { ChevronDown, CloudSun, Droplets, FlaskConical, Info, Leaf, Sprout, ThermometerSun, TriangleAlert } from 'lucide-react'
import MockBadge from './MockBadge'

const riskColor = { low: 'risk-low', medium: 'risk-medium', high: 'risk-high' }

export default function Results({ data }) {
  const [openSnapshot, setOpenSnapshot] = useState(null)
  const [selectedRisk, setSelectedRisk] = useState(0)
  const [selectedCrop, setSelectedCrop] = useState(0)

  if (!data) {
    return (
      <section className="empty-state" aria-live="polite">
        <div className="empty-orbit"><Sprout size={29} /></div>
        <p className="eyebrow">Ready to model</p>
        <h2>Your rotation story starts here.</h2>
        <p>Enter the field details, then run the demo to see how the frontend and API work together.</p>
        <div className="request-preview">
          <span>POST</span><code>/api/farm/analyze</code>
          <span>POST</span><code>/api/rotation/suggest</code>
        </div>
      </section>
    )
  }

  const { analysis, rotation } = data
  const phCheck = analysis.soil.ph_check
  const phRecommended = phCheck?.status === 'Within recommended range'

  return (
    <section className="results" aria-live="polite">
      <div className="results-heading">
        <div>
          <p className="eyebrow">Analysis complete</p>
          <h2>A practical path for your next three seasons.</h2>
        </div>
        <MockBadge />
      </div>

      <div className="insight-grid">
        <button
          type="button"
          className={`insight-card climate-card interactive-card ${openSnapshot === 'climate' ? 'is-open' : ''}`}
          aria-expanded={openSnapshot === 'climate'}
          onClick={() => setOpenSnapshot(openSnapshot === 'climate' ? null : 'climate')}
        >
          <div className="card-label"><CloudSun size={17} /> Climate snapshot</div>
          <ChevronDown className="card-chevron" size={17} />
          <strong>{analysis.climate.average_temperature_c}°C</strong>
          <span>average temperature</span>
          <div className="mini-stats">
            <p><Droplets size={15} /><b>{analysis.climate.annual_rainfall_mm} mm</b> rainfall</p>
            <p><ThermometerSun size={15} /><b>{analysis.climate.growing_season}</b> season</p>
          </div>
          <small>{analysis.climate.source}</small>
          <div className="snapshot-detail">
            <b>How this demo value changes</b>
            <p>This value comes from the adjustable temperature and rainfall controls. Change either control and analyze again to recalculate crop fit and risks.</p>
          </div>
        </button>

        <button
          type="button"
          className={`insight-card soil-card interactive-card ${openSnapshot === 'soil' ? 'is-open' : ''}`}
          aria-expanded={openSnapshot === 'soil'}
          onClick={() => setOpenSnapshot(openSnapshot === 'soil' ? null : 'soil')}
        >
          <div className="card-label"><FlaskConical size={17} /> Soil snapshot</div>
          <ChevronDown className="card-chevron" size={17} />
          <strong>{analysis.soil.texture}</strong>
          <span>soil type</span>
          <div className="soil-line">
            <div><b>{analysis.soil.ph}</b><span>pH</span></div>
            <div><b>{analysis.soil.organic_matter_percent}%</b><span>organic matter</span></div>
          </div>
          <p className={`soil-ph-status ${phCheck ? (phRecommended ? 'is-recommended' : 'is-not-recommended') : ''}`}>
            {phCheck
              ? phRecommended
                ? 'pH is within the recommended range'
                : 'pH is outside the recommended range'
              : 'pH recommendation unavailable'}
          </p>
          {/* <small>{analysis.soil.source}</small> */}

          <div className="snapshot-detail">
            <b>Soil pH advice</b>

            {phCheck ? (
              <>
                <p><strong>{phCheck.status}</strong> ({phCheck.recommended_ph.min}–{phCheck.recommended_ph.max})</p>
                <p>{phCheck.solution}</p>
              </>
            ) : (
              <p>Soil pH advice is not available from the API yet.</p>
            )}
          </div>
        </button>

        <article className="insight-card risk-card">
          <div className="card-label"><TriangleAlert size={17} /> Risk signals</div>
          <div className="risk-list">
            {analysis.risks.map((risk, index) => (
              <button
                type="button"
                key={risk.type}
                className={selectedRisk === index ? 'is-selected' : ''}
                aria-pressed={selectedRisk === index}
                onClick={() => setSelectedRisk(index)}
              >
                <span className={`risk-dot ${riskColor[risk.level]}`} />
                <p><b>{risk.type}</b><small>{risk.level} risk</small></p>
                <ChevronDown size={13} />
              </button>
            ))}
          </div>
          <div className="risk-explanation" aria-live="polite">
            <Info size={14} />
            <p><b>{analysis.risks[selectedRisk].type}</b>{analysis.risks[selectedRisk].note}</p>
          </div>
        </article>
      </div>

      <div className="section-title">
        <div><p className="eyebrow">Crop fit</p><h3>Suggested for this field</h3></div>
        <span>Rule-based score / 100</span>
      </div>
      <div className="crop-list">
        {analysis.suggested_crops.map((crop, index) => (
          <button
            type="button"
            className={`crop-row ${selectedCrop === index ? 'is-selected' : ''}`}
            key={crop.crop}
            aria-pressed={selectedCrop === index}
            onClick={() => setSelectedCrop(index)}
          >
            <div className="crop-rank">0{index + 1}</div>
            <div className="crop-icon"><Leaf size={19} /></div>
            <div className="crop-copy">
              <div><h4>{crop.crop}</h4><span>{crop.water_need_m3_per_dunam} m³/dunam</span></div>
              <p>{crop.reason}</p>
            </div>
            <div className="score" style={{ '--score': `${crop.score}%` }}>
              <b>{crop.score}</b><span>fit</span>
            </div>
          </button>
        ))}
      </div>
      <div className="crop-selection" aria-live="polite">
        <Leaf size={14} />
        <p><b>{analysis.suggested_crops[selectedCrop].crop} selected.</b> Its demo score combines water availability, soil pH, and whether it repeats the previous crop.</p>
      </div>

      <div className="section-title rotation-title">
        <div><p className="eyebrow">Rotation plan</p><h3>{rotation.plan_name}</h3></div>
        <MockBadge compact />
      </div>
      <div className="timeline">
        {rotation.seasons.map((season) => (
          <article className="season" key={season.season}>
            <div className="season-number">{season.season}</div>
            <div className="season-copy">
              <span>{season.period}</span>
              <h4>{season.crop}</h4>
              <p>{season.explanation}</p>
            </div>
          </article>
        ))}
      </div>

      <div className="disclaimer"><Info size={16} /><p>{analysis.disclaimer}</p></div>
    </section>
  )
}
