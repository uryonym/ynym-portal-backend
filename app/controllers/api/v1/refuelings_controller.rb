class Api::V1::RefuelingsController < ApplicationController
  def index
    refuelings = Refueling.order(:created_at)
    render json: refuelings
  end

  def create
    refueling = Refueling.new(refueling_params)
    if refueling.save
      render json: refueling
    else
      render json: refueling.errors
    end
  end

  def update
    refueling = Refueling.find(params[:id])
    if refueling.update(refueling_params)
      render json: refueling
    else
      render json: refueling.errors
    end
  end

  def destroy
    refueling = Refueling.find(params[:id])
    refueling.destroy
    render json: refueling
  end

  private def refueling_params
    params.require(:refueling).permit(
      :id,
      :refuel_datetime,
      :odometer,
      :fuel_type,
      :price,
      :quantity,
      :full_flag,
      :gas_stand,
      :car_id
    )
  end
end
