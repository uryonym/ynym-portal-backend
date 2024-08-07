# frozen_string_literal: true

class Api::V1::CarsController < ApplicationController
  def index
    cars = Car.where(uid: @current_user.uid).order(:seq)
    render(json: cars)
  end

  def create
    car = Car.new(car_params)
    car.uid = @current_user.uid
    if car.save
      render(json: car)
    else
      render(json: car.errors, status: :unprocessable_entity)
    end
  end

  def update
    car = Car.find(params[:id])
    if car.update(car_params)
      render(json: car)
    else
      render(json: car.errors, status: :unprocessable_entity)
    end
  end

  def destroy
    car = Car.find(params[:id])
    car.destroy!
    render(json: car)
  end

  private def car_params
    params.require(:car).permit(
      :id,
      :name,
      :seq,
      :maker,
      :model,
      :model_year,
      :license_plate,
      :tank_capacity,
    )
  end
end
