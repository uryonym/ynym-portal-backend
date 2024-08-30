# frozen_string_literal: true

class Api::V1::RefuelingsController < ApplicationController
  def index
    refuelings = Refueling.where(uid: @current_user.uid, car_id: params[:car_id]).order(refuel_datetime: :desc)
    render(json: refuelings)
  end

  def create
    refueling = Refueling.new(refueling_params)
    refueling.uid = @current_user.uid
    refueling.car_id = params[:car_id]
    if refueling.save
      render(json: refueling)
    else
      render(json: refueling.errors, status: :unprocessable_entity)
    end
  end

  def show
    refueling = Refueling.find(params[:id])
    render(json: refueling)
  end

  def update
    refueling = Refueling.find(params[:id])
    if refueling.update(refueling_params)
      render(json: refueling)
    else
      render(json: refueling.errors, status: :unprocessable_entity)
    end
  end

  def destroy
    refueling = Refueling.find(params[:id])
    refueling.destroy!
    render(json: refueling)
  end

  private def refueling_params
    params.require(:refueling).permit(
      :id,
      :refuel_datetime,
      :odometer,
      :fuel_type,
      :price,
      :total_cost,
      :is_full,
      :gas_stand,
      :car_id,
    )
  end
end
