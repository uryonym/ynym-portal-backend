class Api::V1::SectionsController < ApplicationController
  skip_before_action :authenticate_token

  def index
    sections = Section.order(:seq)
    render json: sections
  end

  def create
    section = Section.new(section_params)
    if section.save
      render json: section
    else
      render json: section.errors
    end
  end

  def show
    section = Section.find(params[:id])
    render json: section
  end

  def update
    section = Section.find(params[:id])
    if section.update(section_params)
      render json: section
    else
      render json: section.errors
    end
  end

  def destroy
    section = Section.find(params[:id])
    section.destroy
    render json: section
  end

  private def section_params
    params.require(:section).permit(:id, :name, :uid, :seq, :note_id)
  end
end
