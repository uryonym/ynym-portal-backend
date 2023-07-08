class Api::V1::ConfidentialsController < ApplicationController
  def index
    confidentials = Confidential.order(:created_at)
    render json: confidentials
  end

  def create
    confidential = Confidential.new(confidential_params)
    if confidential.save
      render json: confidential
    else
      render json: confidential.errors
    end
  end

  def show
    confidential = Confidential.find(params[:id])
    render json: confidential
  end

  def update
    confidential = Confidential.find(params[:id])
    if confidential.update(confidential_params)
      render json: confidential
    else
      render json: confidential.errors
    end
  end

  def destroy
    confidential = Confidential.find(params[:id])
    confidential.destroy
    render json: confidential
  end

  private def confidential_params
    params.require(:confidential).permit(
      :id,
      :service_name,
      :login_id,
      :password,
      :other,
      :created_at,
      :updated_at
    )
  end
end
