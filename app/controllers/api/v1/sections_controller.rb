# frozen_string_literal: true

class Api::V1::SectionsController < ApplicationController
  skip_before_action :authenticate_token

  def index
    sections = Section.where(note_id: params[:note_id]).order(:seq)
    render(json: sections)
  end

  def create
    section = Section.new(section_params)
    section.note_id = params[:note_id]
    if section.save
      render(json: section)
    else
      render(json: section.errors, status: :unprocessable_entity)
    end
  end

  def show
    section = Section.find(params[:id])
    render(json: section)
  end

  def update
    section = Section.find(params[:id])
    if section.update(section_params)
      render(json: section)
    else
      render(json: section.errors, status: :unprocessable_entity)
    end
  end

  def destroy
    section = Section.find(params[:id])
    section.destroy
    render(json: section)
  end

  private def section_params
    params.require(:section).permit(:id, :name, :seq)
  end
end
