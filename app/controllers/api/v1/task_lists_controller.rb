# frozen_string_literal: true

class Api::V1::TaskListsController < ApplicationController
  def index
    task_lists = TaskList.where(uid: @current_user.uid).order(:seq)
    render(json: task_lists)
  end

  def create
    task_list = TaskList.new(task_list_params)
    task_list.uid = @current_user.uid
    if task_list.save
      render(json: task_list)
    else
      render(json: task_list.errors, status: :unprocessable_entity)
    end
  end

  def update
    task_list = TaskList.find(params[:id])
    if task_list.update(task_list_params)
      render(json: task_list)
    else
      render(json: task_list.errors, status: :unprocessable_entity)
    end
  end

  def destroy
    task_list = TaskList.find(params[:id])
    task_list.destroy!
    render(json: task_list)
  end

  private def task_list_params
    params.require(:task_list).permit(
      :id,
      :name,
      :seq,
    )
  end
end
