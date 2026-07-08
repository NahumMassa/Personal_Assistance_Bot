# Personal assistant and finance bot

Main Objective: Create a reliable way to register financial movements to manage personal finances

## How to achive the finance management?

The finance problem is dynamic, we are always fetching new data to analyse. The make this digestible, I decided to uses this metrics as a healtcheck

### Save Rate

$$\text{Tasa de Ahorro} = \left( \frac{\text{Ingresos Mensuales} - \text{Gastos Mensuales}}{\text{Ingresos Mensuales}} \right) \times 100$$

why?
is not a matter of income is, how much you can save. 10% is ok, 20% healthy and 30% is incredible

### Debt-to-Income

$$\text{Índice de Endeudamiento} = \left( \frac{\text{Pagos Mensuales de Deudas}}{\text{Ingreso Mensual Bruto}} \right) \times 100$$
 why?
measures financial leverage (apalancamiento). less than 30% is healthy. if it is more than the 43% is dangerous

### Cobertura del Fondo de Emergencia

$$\text{Meses de Cobertura} = \frac{\text{Total en Fondo de Emergencia (Líquido)}}{\text{Gastos Mensuales Promedio}}$$

why? 
Not looking for revenue, we are trying to find out how much liquidity we have 
between 3-6 months is healthy

### Net Worth (Available in long term)

$$\text{Patrimonio Neto} = \text{Total de Activos} - \text{Total de Pasivos}$$

incomn can be misleading. net worth is a full image of the health status

Frecuencia,Acción / Registro,Objetivo Técnico
Semanal / Diaria,Registro de gastos e ingresos,Minimizar el sesgo de olvido y mantener la integridad de la base de datos.
Mensual,Cálculo de Tasa de Ahorro y Balance de Mes,Evaluar desviaciones respecto al presupuesto asignado.
Trimestral / Anual,Actualización de Patrimonio Neto y Fondo de Emergencia,Monitorear el crecimiento macro de tu patrimonio y ajustar por inflación o cambios de estilo de vida.

## Workflows

### Finance

1. The user inputs all the expenses and incomes of money via a telgram bot and their categories.
2. The API register the movement into the db
3. Data is consulted in the dashboard

### Assitant

1. Retrive all pending task in microsoft teams
2. Save them in the db
3. Send a remainder to telegram

