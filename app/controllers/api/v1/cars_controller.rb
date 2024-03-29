class Api::V1::CarsController < ApplicationController
  def index
    cars = Car.order(:name)
    render json: cars
  end

  def create
    car = Car.new(car_params)
    if car.save
      render json: car
    else
      render json: car.errors
    end
  end

  def show
    car = Car.find(params[:id])
    render json: car
  end

  def update
    car = Car.find(params[:id])
    if car.update(car_params)
      render json: car
    else
      render json: car.errors
    end
  end

  def destroy
    car = Car.find(params[:id])
    car.destroy
    render json: car
  end

  private def car_params
    params.require(:car).permit(
      :id,
      :name,
      :maker,
      :model,
      :model_year,
      :license_plate,
      :tank_capacity
    )
  end
end
